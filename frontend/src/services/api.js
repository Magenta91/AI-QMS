import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/api/complaints/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const processComplaint = async (text, sourceType = 'text') => {
  const response = await api.post('/api/complaints/process', {
    text,
    source_type: sourceType,
  });
  
  return response.data;
};

export const correctComplaint = async (complaintData, userMessage, field = null) => {
  const response = await api.post('/api/complaints/correct', {
    complaint_data: complaintData,
    user_message: userMessage,
    field,
  });
  
  return response.data;
};

export const assessRisk = async (complaintData) => {
  const response = await api.post('/api/risk/assess', complaintData);
  return response.data;
};

export const saveComplaint = async (complaintData) => {
  const response = await api.post('/api/complaints', complaintData);
  return response.data;
};

export const getComplaint = async (id) => {
  const response = await api.get(`/api/complaints/${id}`);
  return response.data;
};

export default api;
