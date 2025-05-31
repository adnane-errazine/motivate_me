
import { useState, useRef, KeyboardEvent } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Paperclip, Send, X, FileText } from "lucide-react";
import { cn } from "@/lib/utils";

interface MessageInputProps {
  onSendMessage: (content: string, images?: File[]) => void;
  isLoading: boolean;
}

const MessageInput = ({ onSendMessage, isLoading }: MessageInputProps) => {
  const [message, setMessage] = useState("");
  const [attachedFiles, setAttachedFiles] = useState<File[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (message.trim() || attachedFiles.length > 0) {
      onSendMessage(message.trim(), attachedFiles);
      setMessage("");
      setAttachedFiles([]);
      
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileSelect = (files: FileList | null) => {
    if (files) {
      const allowedFiles = Array.from(files).filter(file =>
        file.type.startsWith("image/") || file.type === "application/pdf"
      );
      setAttachedFiles(prev => [...prev, ...allowedFiles]);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const removeFile = (index: number) => {
    setAttachedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  };

  const renderFilePreview = (file: File, index: number) => {
    if (file.type.startsWith("image/")) {
      return (
        <div
          key={index}
          className="relative group bg-white rounded-lg p-2 shadow-sm border border-gray-200"
        >
          <img
            src={URL.createObjectURL(file)}
            alt={file.name}
            className="w-16 h-16 object-cover rounded"
          />
          <button
            onClick={() => removeFile(index)}
            className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <X size={12} />
          </button>
        </div>
      );
    } else if (file.type === "application/pdf") {
      return (
        <div
          key={index}
          className="relative group bg-white rounded-lg p-2 shadow-sm border border-gray-200 flex items-center space-x-2"
        >
          <FileText className="w-8 h-8 text-red-500" />
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium text-gray-900 truncate">{file.name}</p>
            <p className="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
          <button
            onClick={() => removeFile(index)}
            className="bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <X size={12} />
          </button>
        </div>
      );
    }
  };

  return (
    <div
      className={cn(
        "relative border-2 border-dashed rounded-2xl transition-all duration-200",
        isDragOver
          ? "border-blue-400 bg-blue-50"
          : "border-transparent bg-gray-50"
      )}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
    >
      {/* Drag overlay */}
      {isDragOver && (
        <div className="absolute inset-0 bg-blue-100/50 rounded-2xl flex items-center justify-center z-10">
          <p className="text-blue-600 font-medium">Drop images or PDFs here</p>
        </div>
      )}

      {/* Attached files preview */}
      {attachedFiles.length > 0 && (
        <div className="flex flex-wrap gap-2 p-3 border-b border-gray-200">
          {attachedFiles.map((file, index) => renderFilePreview(file, index))}
        </div>
      )}

      {/* Input area */}
      <div className="flex place-items-center gap-2 p-3">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => fileInputRef.current?.click()}
          className="flex-shrink-0 text-gray-500 hover:text-gray-700"
          disabled={isLoading}
        >
          <Paperclip size={20} />
        </Button>

        <Textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => {
            setMessage(e.target.value);
            adjustTextareaHeight();
          }}
          onKeyDown={handleKeyDown}
          placeholder="Type your message here..."
          className="flex-1 resize-none border-none bg-transparent focus:ring-0 focus:outline-none min-h-[24px] max-h-[200px]"
          disabled={isLoading}
          style={{ height: "auto" }}
        />

        <Button
          onClick={handleSend}
          disabled={isLoading || (!message.trim() && attachedFiles.length === 0)}
          className="flex-shrink-0 bg-blue-400 hover:bg-blue-700 text-white rounded-full w-10 h-10 p-0"
        >
          <Send size={16} />
        </Button>
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept="image/*,.pdf"
        onChange={(e) => handleFileSelect(e.target.files)}
        className="hidden"
      />
    </div>
  );
};

export default MessageInput;
