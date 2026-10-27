function ErrorMessage({ message }) {
  return (
    <div className="error-message">
      {message || "Something went wrong."}
    </div>
  );
}

export default ErrorMessage;