import { createSlice } from "@reduxjs/toolkit";

const slice = createSlice({
  name:"copilot",
  initialState:{messages:[],isProcessing:false,error:null},
  reducers:{
    addMessage(state,action){state.messages.push(action.payload)},
    setProcessing(state,action){state.isProcessing=action.payload},
    setError(state,action){state.error=action.payload}
  }
});
export const {addMessage,setProcessing,setError}=slice.actions;
export default slice.reducer;
