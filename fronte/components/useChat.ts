import { chatApi } from "@/lib/api";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { HistoryDTO } from "@/types/message";
import { useSearchParams } from "next/navigation";

export const useChat = () => {
  const searchparams = useSearchParams();

  if (searchparams.get("id") === null) {
    throw new Error("Session ID is required");
  }

  const [inputV, setInputV] = useState("");

  const [messages, setMessages] = useState<HistoryDTO[]>([]);

  const handleChangeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputV(e.target.value);
  };

  const { mutate, isPending } = useMutation({
    mutationFn: (data: string) => {
      const formData = new FormData();
      formData.append("message", data);
      formData.append("session_id", searchparams.get("id") || "");
      return chatApi
        .sendMessage(formData)
        .then((res) => {
          setMessages((prev) => [
            ...prev,
            {
              message: data,
              assistant_response: res.content,
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
