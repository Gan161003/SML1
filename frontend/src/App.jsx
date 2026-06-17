// import { BrowserRouter, Routes, Route } from "react-router-dom";

// import MainLayout from "./layouts/MainLayout";

// import Dashboard from "./pages/Dashboard";
// import Home from "./pages/Home";
// import Track from "./pages/Track";
// import Mentions from "./pages/Mentions";
// import Reports from "./pages/Reports";
// import DataCenter from "./pages/DataCenter";
// import Settings from "./pages/Settings";
// import Alerts from "./pages/Alerts";

// function App() {
//   return (
//     <BrowserRouter>
//       <Routes>
//         <Route element={<MainLayout />}>
//           <Route path="/" element={<Home />} />
//           <Route path="/" element={<Dashboard />} />
//           <Route path="/track" element={<Track />} />
//           <Route path="/mentions" element={<Mentions />} />
//           <Route path="/reports" element={<Reports />} />
//           <Route path="/datacenter" element={<DataCenter />} />
//           <Route path="/Alerts" element={<Alerts />} />
//           <Route path="/settings" element={<Settings />} />
//         </Route>
//       </Routes>
//     </BrowserRouter>
//   );
// }

// export default App;



import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Track from "./pages/Track";
import Mentions from "./pages/Mentions";
import Reports from "./pages/Reports";
import DataCenter from "./pages/DataCenter";
import Settings from "./pages/Settings";
import Alerts from "./pages/Alerts";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route element={<MainLayout />}>

          <Route
            path="/"
            element={<Home />}
          />

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/track"
            element={<Track />}
          />

          <Route
            path="/mentions"
            element={<Mentions />}
          />

          <Route
            path="/reports"
            element={<Reports />}
          />

          <Route
            path="/datacenter"
            element={<DataCenter />}
          />

          <Route
            path="/alerts"
            element={<Alerts />}
          />

          <Route
            path="/settings"
            element={<Settings />}
          />

        </Route>

      </Routes>

    </BrowserRouter>

  );

}

export default App;