export interface Message {
  id: string;
  content: string;
  sender: "user" | "bot";
  timestamp: Date;
}

export interface SendMessageDTO {
  message: string;
  history: HistoryDTO[];
}

export interface HistoryDTO {
  message: string;
  assistant_response: string;
}

export interface ReceiveMessageDTO {
  detail: string;
}
