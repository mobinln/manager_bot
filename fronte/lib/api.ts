import axios from "axios";
import { SendMessageDTO, ReceiveMessageDTO } from "@/types/message";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://192.168.213.82:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const chatApi = {
  sendMessage: async (data: SendMessageDTO): Promise<ReceiveMessageDTO> => {
    const response = await api.post<ReceiveMessageDTO>("/chat/completion", data);
    return response.data;
  },
};
