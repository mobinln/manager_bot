export interface Message {
  id: string;
  content: string;
  sender: "user" | "bot";
  timestamp: Date;
}

export interface SendMessageDTO {
  message: string;
  session_id: string;
}

export interface HistoryDTO {
  message: string;
  assistant_response: string;
}

export interface ReceiveMessageDTO {
  content: string;
}
