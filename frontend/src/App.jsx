import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import ShipmentDetails from "./pages/ShipmentDetails";
import Decisions from "./pages/Decisions";
import Outcomes from "./pages/Outcomes";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/shipments/:id" element={<ShipmentDetails />} />
        <Route path="/decisions" element={<Decisions />} />
        <Route path="/outcomes" element={<Outcomes />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;