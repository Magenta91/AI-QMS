# 💬 AI Chat Feature - User Guide

## ✅ Feature Now Working!

The "Ask me anything about this complaint" chat feature is now fully functional.

---

## 🎯 What You Can Do

### 1. Ask Questions
Get information about the current complaint:

**Examples:**
- "What's the risk level of this complaint?"
- "Is the complaint data complete?"
- "What fields are missing?"
- "What product is this about?"
- "Who is the customer?"
- "What's the batch number?"

### 2. Correct/Update Fields
Make conversational corrections to the complaint:

**Examples:**
- "Change the batch number to AMX-2024-002"
- "The customer name should be ABC Hospital"  
- "Update the priority to High"
- "Set the expiry date to 2025-12-31"
- "The manufacturing date is wrong, it should be 2024-01-15"

### 3. Get Guidance
Ask for help understanding the complaint:

**Examples:**
- "What information is most important here?"
- "Should I update anything?"
- "What's the recommended action?"
- "Is this ready to save?"

---

## 🚀 How to Use

### Step 1: Upload a Complaint
First, upload a PDF document so there's complaint data to work with.

### Step 2: Type Your Message
In the chat box at the bottom of the AI Copilot panel:
1. Click in the input field
2. Type your question or instruction
3. Press **Enter** or click the **➤** button

### Step 3: See the Response
- AI processes your message (2-5 seconds)
- Response appears in the message history
- If you made a correction, the form updates automatically

---

## 📋 Example Conversations

### Example 1: Asking Questions

**You**: "What's the risk level?"  
**AI**: "The current risk level is HIGH due to foreign matter contamination, which poses direct patient safety concerns."

**You**: "What fields are missing?"  
**AI**: "The following fields are missing: Originating Site, Affected Material."

### Example 2: Making Corrections

**You**: "Change the batch number to AMX-2024-NEW"  
**AI**: "I've updated the batch number to AMX-2024-NEW"  
*[Form automatically updates]*

**You**: "The customer name should be General Hospital"  
**AI**: "I've updated the customer name to General Hospital"  
*[Form field changes immediately]*

### Example 3: Complex Requests

**You**: "Update priority to High and severity to Critical"  
**AI**: "I've updated the priority to High"  
*[Note: Currently handles one field at a time]*

---

## 🎨 UI Features

### Message Display
- **System messages** (gray): Upload status, extraction progress
- **AI messages** (black, bold): AI responses
- **Your messages** (blue, bold): Your questions/requests

### Chat Input
- Type your message in the text box
- Press Enter to send
- Button disabled while processing
- Input disabled while AI is working

### Message History
- Shows last 5 messages
- Scrolls automatically
- Clears when you refresh page

---

## 💡 Pro Tips

### For Best Results:

1. **Be Specific**: "Change batch number to X" works better than "Fix the batch"
2. **One at a Time**: Update one field per message for accuracy
3. **Upload First**: Chat works best after uploading a document
4. **Use Field Names**: Say "batch number" or "customer name" not "the batch thing"

### Common Field Names:
- complaint_source
- customer_name
- product_name
- product_strength
- batch_number
- affected_quantity
- manufacturing_date
- expiry_date
- complaint_date
- originating_site
- complaint_type
- complaint_description
- initial_severity
- priority

### What Works:
✅ "What's the risk level?"  
✅ "Change batch number to AMX-001"  
✅ "Is this complete?"  
✅ "Update customer name to ABC Corp"  

### What to Improve:
⚠️ "Fix everything" - Too vague  
⚠️ "Change batch and date" - One field at a time  
⚠️ "Make it better" - Be specific  

---

## 🔧 Technical Details

### How It Works

1. **You send a message** → Frontend sends to backend
2. **AI analyzes intent** → Determines if question or correction
3. **AI processes** → Either answers or updates fields
4. **Response returns** → UI updates with answer/changes
5. **Form updates** → If correction, fields auto-update

### Processing Time
- **Questions**: 2-4 seconds
- **Corrections**: 3-5 seconds
- **Complex requests**: 5-8 seconds

### AI Model
- Uses `openai/gpt-oss-120b` via Groq
- Temperature: 0.3 (balanced accuracy)
- Max tokens: 500 (concise responses)

---

## 🐛 Troubleshooting

### Chat input doesn't work
**Solution**: Make sure you've uploaded a document first. The chat needs complaint data to work with.

### "Please upload a complaint document first"
**Cause**: No complaint data loaded  
**Solution**: Upload a PDF from the samples folder

### Response takes too long
**Cause**: AI model processing, network latency  
**Solution**: Wait up to 10 seconds. Check backend logs if it times out.

### Field doesn't update
**Cause**: AI didn't recognize the field name or value  
**Solution**: 
- Use exact field names listed above
- Be more specific: "Change batch_number to AMX-001"
- Check the message response for what AI understood

### Chat is disabled
**Cause**: AI is currently processing  
**Solution**: Wait for current operation to complete

---

## 📊 Features Comparison

| Feature | Status | Notes |
|---------|--------|-------|
| Ask questions | ✅ Working | About current complaint |
| Single field correction | ✅ Working | Update one field at a time |
| Multi-field correction | ⚠️ Partial | Works but processes one field |
| Field validation | ✅ Working | Checks field names |
| Context awareness | ✅ Working | Knows current complaint state |
| Message history | ✅ Working | Last 5 messages shown |
| Typing indicators | ❌ Not yet | Future enhancement |
| Suggested questions | ❌ Not yet | Future enhancement |

---

## 🎯 Testing the Feature

### Quick Test:
1. Upload `samples/complaint_005_minor_issue.pdf`
2. Wait for extraction to complete
3. Type: "What's the product name?"
4. Press Enter
5. See AI respond with the product name

### Correction Test:
1. After uploading a complaint
2. Type: "Change the priority to High"
3. Press Enter
4. Watch the Priority field update in the form
5. See confirmation message from AI

---

## 🚀 Future Enhancements (Not in MVP)

Potential improvements:
- [ ] Multi-field updates in one message
- [ ] Voice input for chat
- [ ] Suggested questions based on context
- [ ] Chat history persistence
- [ ] Export chat transcript
- [ ] Undo/redo corrections
- [ ] Field-specific chat triggers
- [ ] Autocomplete for field names

---

## ✅ Status

**Current Status**: ✅ Fully Operational

- Chat input: Working
- Send button: Working  
- Enter key: Working
- AI responses: Working
- Field corrections: Working
- Message history: Working
- Loading states: Working

**Ready for**: Testing, demos, interviews

---

**Try it now at**: http://localhost:5173

Upload a sample and start chatting! 💬
