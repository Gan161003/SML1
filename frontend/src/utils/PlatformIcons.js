import {
  FaInstagram,
  FaYoutube,
  FaReddit,
  FaRss,
  FaNewspaper,
  FaGoogle
} from "react-icons/fa";

export const getPlatformIcon = (
  connectorType
) => {

  const type = String(
    connectorType || ""
  ).toLowerCase();

  if (type.includes("instagram")) {
    return <FaInstagram color="#E4405F" />;
  }

  if (type.includes("youtube")) {
    return <FaYoutube color="#FF0000" />;
  }

  if (type.includes("reddit")) {
    return <FaReddit color="#FF4500" />;
  }

  if (type.includes("rss")) {
    return <FaRss color="#F97316" />;
  }

  if (type.includes("news")) {
    return <FaNewspaper color="#2563EB" />;
  }

  if (type.includes("google")) {
    return <FaGoogle color="#4285F4" />;
  }

  return "🔗";
};