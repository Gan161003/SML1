import { Link } from "react-router-dom";

// import {
//   FaHome,
//   FaChartBar,
//   // FaSearch,
//   FaComments,
//   FaFileAlt,
//   FaDatabase,
//   // FaBell,
//   // FaCog
// } from "react-icons/fa";
import {
  FaHome,
  FaChartBar,
  FaComments,
  FaFileAlt,
  FaDatabase
} from "react-icons/fa";

import "./Header.css";

function Header() {
  return (
    <header className="main-header">

      <Link to="/" className="logo">
        Social Listening Platform
      </Link>

      <nav className="nav-menu">

        <Link to="/">
          <FaHome />
          <span>Home</span>
        </Link>

        <Link to="/dashboard">
          <FaChartBar />
          <span>Dashboard</span>
        </Link>

        {/* <Link to="/track">
          <FaSearch />
          <span>Track</span>
        </Link> */}

        <Link to="/mentions">
          <FaComments />
          <span>Mentions</span>
        </Link>

        <Link to="/reports">
          <FaFileAlt />
          <span>Reports</span>
        </Link>

        <Link to="/datacenter">
          <FaDatabase />
          <span>Data Center</span>
        </Link>

        {/* <Link to="/alerts">
          <FaBell />
          <span>Alerts</span>
        </Link>

        <Link to="/settings">
          <FaCog />
          <span>Settings</span>
        </Link> */}

      </nav>

    </header>
  );
}

export default Header;