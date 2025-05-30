import { chatApi } from "@/lib/api";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { HistoryDTO } from "@/types/message";

export const useChat = () => {
  const [inputV, setInputV] = useState("");

  const [messages, setMessages] = useState<HistoryDTO[]>([]);

  const handleChangeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputV(e.target.value);
  };

  const { mutate, isPending } = useMutation({
    mutationFn: (data: string) => {
      return chatApi
        .sendMessage({
          message: data,
          history: messages,
        })
        .then((res) => {
          setMessages((prev) => [
            ...prev,
            {
              message: data,
              assistant_response: res.detail,
            },
          ]);
        })
        .finally(() => {
          setInputV("");
        });
    },
    mutationKey: ["/chat", inputV],
  });

  const handleSubmit = (e: any) => {
    e.preventDefault();
    mutate(inputV);
  };

  return {
    handleSubmit,
    inputV,
    handleChangeInput,
    messages,
    isTyping: isPending,
  };
};
