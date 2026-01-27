import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const scanImage = async (fileBlob: Blob, lang: string) => {
  const formData = new FormData();
  formData.append("file", fileBlob, "scan.jpg");
  
  const response = await axios.post(`${API_BASE_URL}/scan?lang=${lang}`, formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  
  return response.data;
};