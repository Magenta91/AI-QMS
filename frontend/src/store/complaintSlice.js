import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  complaint_source:"", customer_name:"", product_name:"", product_strength:"",
  batch_number:"", affected_quantity:"", manufacturing_date:"", expiry_date:"",
  complaint_date:"", originating_site:"", affected_material:"", complaint_type:"",
  complaint_description:"", initial_severity:"", priority:"", risk_level:""
};

const slice = createSlice({
  name:"complaint", initialState,
  reducers:{
    setField(state, action){ state[action.payload.key] = action.payload.value; },
    setComplaint(state, action){ Object.assign(state, action.payload); },
    resetComplaint(){ return initialState; }
  }
});
export const {setField,setComplaint,resetComplaint} = slice.actions;
export default slice.reducer;
