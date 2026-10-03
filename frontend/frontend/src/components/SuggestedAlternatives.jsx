import { useState } from "react";

function SuggestedAlternatives() {

  const [selected, setSelected] = useState("shipping");
  const [saved, setSaved] = useState(false);

  const options = [
    {
      id: "shipping",
      title: "Faster Shipping",
      description: "Extra Cost: +$2,500 | Delay: 2 days"
    },
    {
      id: "supplier",
      title: "Alternate Supplier",
      description: "Extra Cost: +$1,200 | Delay: 4 days"
    },
    {
      id: "launch",
      title: "Adjust Launch Plan",
      description: "Extra Cost: $0 | Delay: 7 days"
    }
  ];

  function saveDecision() {
    setSaved(true);

    setTimeout(() => {
      setSaved(false);
    }, 2000);
  }

  return (
    <div className="panel">

      <h3>Suggested Alternatives</h3>

      <p>
        Shipment: <strong>SHP001</strong> (High Risk)
      </p>

      {options.map((option) => (

        <label key={option.id} className="alternative">

          <input
            type="radio"
            name="decision"
            checked={selected === option.id}
            onChange={() => setSelected(option.id)}
          />

          <div>
            <strong>{option.title}</strong>
            <p>{option.description}</p>
          </div>

        </label>

      ))}

      <button
        className="save-button"
        onClick={saveDecision}
      >
        {saved ? "Decision Saved ✓" : "Save Decision"}
      </button>

    </div>
  );
}

export default SuggestedAlternatives;