import Header from "../components/Header";
import { Outlet } from "react-router-dom";

function MainLayout() {
  return (
    <>
      <Header />

      <main className="page-container">
        <Outlet />
      </main>
    </>
  );
}

export default MainLayout;

