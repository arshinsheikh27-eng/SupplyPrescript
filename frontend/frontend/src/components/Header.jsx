import { UserCircle } from "lucide-react";

function Header() {
  return (
    <header className="header">

      <div>
        <h1>Welcome, Team!</h1>

        <p>
          Here's the latest shipment insights and recommendations.
        </p>
      </div>

      <div className="user-profile">
        <UserCircle size={30} />
        <span>Team</span>
      </div>

    </header>
  );
}

export default Header;