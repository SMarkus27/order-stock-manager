export function Feedback({ error, successMessage, onClose }) {
  const message = error ?? successMessage;

  if (!message) {
    return null;
  }

  return (
    <div className={error ? "feedback error" : "feedback success"} role="status">
      <span>{message}</span>
      <button type="button" onClick={onClose} aria-label="Fechar mensagem">
        x
      </button>
    </div>
  );
}
