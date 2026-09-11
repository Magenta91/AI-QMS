import { useDispatch, useSelector } from "react-redux";
import { setField, setComplaint } from "./store/complaintSlice";
import { addMessage, setProcessing, setError } from "./store/copilotSlice";
import { uploadDocument, processComplaint, assessRisk, correctComplaint, saveComplaint } from "./services/api";
import { useState, useRef } from "react";

const fields = [
["complaint_source","Complaint Source"],["customer_name","Customer Name"],
["product_name","Product Name"],["product_strength","Product Strength / Grade"],
["batch_number","Batch / Lot Number"],["affected_quantity","Affected Quantity"],
["manufacturing_date","Manufacturing Date"],["expiry_date","Expiry Date"],
["complaint_date","Complaint Date"],["originating_site","Originating Site"],
["complaint_type","Complaint Type"],["initial_severity","Initial Severity"],
["priority","Priority"]
];

export default function App(){
 const dispatch=useDispatch();
 const complaint=useSelector(s=>s.complaint);
 const copilot=useSelector(s=>s.copilot);
 const [uploadStatus, setUploadStatus] = useState("");
 const [riskAssessment, setRiskAssessment] = useState(null);
 const [chatInput, setChatInput] = useState("");
 const fileInputRef = useRef(null);
 
 const handleFileSelect = () => {
   fileInputRef.current?.click();
 };
 
 const handleFileUpload = async (e) => {
   const file = e.target.files?.[0];
   if (!file) return;
   
   setUploadStatus("Uploading and extracting text...");
   dispatch(setProcessing(true));
   dispatch(addMessage({ role: "system", content: `Uploading ${file.name}...` }));
   
   try {
     // Upload and extract text from PDF
     const uploadResult = await uploadDocument(file);
     dispatch(addMessage({ 
       role: "system", 
       content: `Extracted ${uploadResult.char_count} characters from ${file.name}` 
     }));
     
     setUploadStatus("Processing through AI workflow...");
     
     // Process through LangGraph
     const processResult = await processComplaint(uploadResult.extracted_text, 'pdf');
     
     if (processResult.complaint) {
       dispatch(setComplaint(processResult.complaint));
       dispatch(addMessage({ 
         role: "assistant", 
         content: "Successfully extracted complaint details from document!" 
       }));
     }
     
     // Get risk assessment
     if (processResult.complaint) {
       setUploadStatus("Performing risk assessment...");
       const risk = await assessRisk(processResult.complaint);
       setRiskAssessment(risk);
     }
     
     setUploadStatus("Complete!");
     dispatch(setProcessing(false));
     
   } catch (error) {
     console.error("Upload error:", error);
     dispatch(setError(error.message || "Upload failed"));
     dispatch(addMessage({ 
       role: "system", 
       content: `Error: ${error.response?.data?.detail || error.message}` 
     }));
     setUploadStatus("Upload failed");
     dispatch(setProcessing(false));
   }
 };
 
 const handleChatSubmit = async () => {
   if (!chatInput.trim()) return;
   
   const userMessage = chatInput.trim();
   setChatInput("");
   
   // Add user message to chat
   dispatch(addMessage({ role: "user", content: userMessage }));
   dispatch(setProcessing(true));
   
   try {
     // Check if there's complaint data to work with
     const hasComplaintData = Object.values(complaint).some(val => val);
     
     if (!hasComplaintData) {
       dispatch(addMessage({ 
         role: "assistant", 
         content: "Please upload a complaint document first, or I can help you understand the system. What would you like to know?" 
       }));
       dispatch(setProcessing(false));
       return;
     }
     
     // Call the correction/chat API
     const result = await correctComplaint(complaint, userMessage);
     
     if (result.complaint) {
       // Update complaint with corrected data
       dispatch(setComplaint(result.complaint));
       dispatch(addMessage({ 
         role: "assistant", 
         content: "I've updated the complaint based on your request. Please review the changes." 
       }));
       
       // Re-assess risk if complaint changed
       const risk = await assessRisk(result.complaint);
       setRiskAssessment(risk);
     } else {
       dispatch(addMessage({ 
         role: "assistant", 
         content: "I understood your message. How else can I help with this complaint?" 
       }));
     }
     
   } catch (error) {
     console.error("Chat error:", error);
     dispatch(addMessage({ 
       role: "assistant", 
       content: `I encountered an error: ${error.response?.data?.detail || error.message}. Please try rephrasing your question.` 
     }));
   } finally {
     dispatch(setProcessing(false));
   }
 };
 
 const handleChatKeyPress = (e) => {
   if (e.key === 'Enter' && !e.shiftKey) {
     e.preventDefault();
     handleChatSubmit();
   }
 };
 
 const handleSaveComplaint = async () => {
   // Check if there's complaint data to save
   const hasData = Object.values(complaint).some(val => val);
   
   if (!hasData) {
     dispatch(addMessage({ 
       role: "system", 
       content: "No complaint data to save. Please upload a document or enter data manually." 
     }));
     return;
   }
   
   // Check for required fields
   const requiredFields = ["product_name", "batch_number", "complaint_description"];
   const missing = requiredFields.filter(field => !complaint[field]);
   
   if (missing.length > 0) {
     const fieldNames = missing.map(f => f.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()));
     const confirmed = window.confirm(
       `The following required fields are missing:\n${fieldNames.join(', ')}\n\nDo you want to save anyway?`
     );
     if (!confirmed) return;
   }
   
   dispatch(setProcessing(true));
   dispatch(addMessage({ role: "system", content: "Saving complaint..." }));
   
   try {
     const result = await saveComplaint(complaint);
     
     dispatch(addMessage({ 
       role: "system", 
       content: `Complaint saved successfully! ID: ${result.id || 'N/A'}` 
     }));
     
     // Show success message
     alert(`Complaint saved successfully!\n\nComplaint ID: ${result.id || 'Generated'}\n\nThe complaint has been recorded in the system.`);
     
   } catch (error) {
     console.error("Save error:", error);
     dispatch(setError(error.message || "Save failed"));
     dispatch(addMessage({ 
       role: "system", 
       content: `Error saving complaint: ${error.response?.data?.detail || error.message}` 
     }));
     alert(`Failed to save complaint:\n${error.response?.data?.detail || error.message}`);
   } finally {
     dispatch(setProcessing(false));
   }
 };
 
 return <main className="app-shell">
  <header className="topbar">
   <div><h1>AIVOA Complaint Management</h1><p>AI-assisted pharmaceutical customer complaint intake</p></div>
   <span className="status-badge">Pending Triage</span>
  </header>
  <section className="workspace">
   <section className="card">
    <div className="card-header"><h2>Log Customer Complaint</h2><span>AI-assisted extraction</span></div>
    <div className="form-grid">
     {fields.map(([key,label])=><label key={key}><span>{label}</span>
      <input value={complaint[key]||""} placeholder="Awaiting AI extraction..."
       onChange={e=>dispatch(setField({key,value:e.target.value}))}/></label>)}
     <label className="full-width"><span>Complaint Description</span>
      <textarea value={complaint.complaint_description||""} placeholder="Awaiting AI extraction..."
       onChange={e=>dispatch(setField({key:"complaint_description",value:e.target.value}))}/></label>
    </div>
    <button 
      className="primary-button"
      onClick={handleSaveComplaint}
      disabled={copilot.isProcessing}
    >
      {copilot.isProcessing ? "Saving..." : "Save Complaint"}
    </button>
   </section>
   <aside className="card">
    <div className="card-header"><h2>AI Copilot</h2><span className="beta">BETA</span></div>
    <div className="upload-box">
     <strong>Upload complaint document</strong>
     <p>PDF / DOCX / TXT / email text</p>
     <input 
       type="file" 
       ref={fileInputRef}
       onChange={handleFileUpload}
       accept=".pdf"
       style={{display: 'none'}}
     />
     <button 
       className="secondary-button" 
       onClick={handleFileSelect}
       disabled={copilot.isProcessing}
     >
       {copilot.isProcessing ? "Processing..." : "Choose File"}
     </button>
     {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
    </div>
    <div className="assistant-message">
     <strong>AI Assistant</strong>
     {copilot.messages.length > 0 ? (
       <div className="messages">
         {copilot.messages.slice(-5).map((msg, idx) => (
           <p key={idx} className={`message-${msg.role}`}>
             {msg.role === 'user' && <strong>You: </strong>}
             {msg.content}
           </p>
         ))}
       </div>
     ) : (
       <p>Upload a complaint document or paste complaint text. The AI workflow will extract details and populate the form.</p>
     )}
    </div>
    <div className="risk-panel">
     <strong>AI Risk Assessment</strong>
     {riskAssessment ? (
       <div className="risk-result">
         <span className={`risk-level risk-${riskAssessment.risk_level?.toLowerCase()}`}>
           {riskAssessment.risk_level}
         </span>
         <p><strong>Reasons:</strong></p>
         <ul>
           {riskAssessment.reasons?.map((reason, idx) => (
             <li key={idx}>{reason}</li>
           ))}
         </ul>
         <p><strong>Recommended Action:</strong> {riskAssessment.recommended_action}</p>
       </div>
     ) : (
       <span>Awaiting assessment</span>
     )}
    </div>
    <div className="chat-box">
     <input 
       placeholder="Ask me anything about this complaint..."
       value={chatInput}
       onChange={(e) => setChatInput(e.target.value)}
       onKeyPress={handleChatKeyPress}
       disabled={copilot.isProcessing}
     />
     <button 
       className="send-button"
       onClick={handleChatSubmit}
       disabled={copilot.isProcessing || !chatInput.trim()}
     >
       ➤
     </button>
    </div>
   </aside>
  </section>
 </main>;
}
