"use client";

import { Chat } from "@/components/Chat";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();
export default function ChatbotUI() {
  return (
    <QueryClientProvider client={queryClient}>
      <Chat />;
    </QueryClientProvider>
  );
}
