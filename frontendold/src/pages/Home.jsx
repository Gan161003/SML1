import React from "react";
import { useNavigate } from "react-router-dom";
import {
  FaInstagram,
  FaYoutube,
  FaNewspaper,
  FaStar,
  FaBullhorn,
  FaSearch,
  FaChartLine,
  FaBrain,
  FaRobot,
  FaComments
} from "react-icons/fa";

import "../styles/Home.css";

export default function Home() {
  const navigate = useNavigate();

  const platforms = [
    { icon: <FaInstagram />, name: "Instagram" },
    { icon: <FaYoutube />, name: "YouTube" },
    { icon: <FaNewspaper />, name: "News" },
    { icon: <FaStar />, name: "Reviews" },
    { icon: <FaBullhorn />, name: "Campaign India" }
  ];

  const features = [
    {
      icon: <FaBrain />,
      title: "Sentiment Analysis",
      desc: "Understand public opinion with AI powered sentiment detection."
    },
    {
      icon: <FaRobot />,
      title: "Trend Discovery",
      desc: "Identify emerging discussions before they become mainstream."
    },
    {
      icon: <FaComments />,
      title: "Conversation Tracking",
      desc: "Monitor discussions happening across multiple channels."
    },
    {
      icon: <FaChartLine />,
      title: "Insight Generation",
      desc: "Transform raw conversations into meaningful intelligence."
    }
  ];

  return (

    <div className="home-page">

      {/* HERO */}

      <section className="hero-section">

        <div className="hero-content">

          <h1>
            Listen Beyond
            <span> Social Media</span>
          </h1>

          <p>
            Transform conversations into actionable insights
            across social media, news, reviews and digital channels.
          </p>

          <div className="hero-buttons">

            <button
              className="primary-btn"
              onClick={() => navigate("/dashboard")}
            >
              Start Monitoring
            </button>

            <button
              className="secondary-btn"
              onClick={() => navigate("/mentions")}
            >
              Explore Platform
            </button>

          </div>

        </div>

      </section>

      {/* PLATFORMS */}

      <section className="platform-section">

        <h2>What We Monitor</h2>

        <div className="platform-grid">

          {platforms.map((item, index) => (

            <div
              key={index}
              className="platform-card"
            >

              <div className="platform-icon">
                {item.icon}
              </div>

              <h3>
                {item.name}
              </h3>

            </div>

          ))}

        </div>

      </section>

      {/* JOURNEY */}

      <section className="journey-section">

        <h2>
          Monitoring Journey
        </h2>

        <div className="journey-flow">

          <div>Track</div>
          <span>→</span>

          <div>Collect</div>
          <span>→</span>

          <div>Clean</div>
          <span>→</span>

          <div>Analyze</div>
          <span>→</span>

          <div>Detect</div>
          <span>→</span>

          <div>Report</div>

        </div>

      </section>

      {/* FEATURES */}

      <section className="feature-section">

        <h2>
          AI Intelligence
        </h2>

        <div className="feature-grid">

          {features.map((item, index) => (

            <div
              key={index}
              className="feature-card"
            >

              <div className="feature-icon">
                {item.icon}
              </div>

              <h3>
                {item.title}
              </h3>

              <p>
                {item.desc}
              </p>

            </div>

          ))}

        </div>

      </section>

      {/* ECOSYSTEM */}

      <div className="ecosystem-network">

        <div className="node top">Instagram</div>

        <div className="middle-row">
          <div className="node">Reviews</div>

          <div className="center-node">
            Brand
          </div>

          <div className="node">News</div>
        </div>

        <div className="bottom-row">
          <div className="node">YouTube</div>

          <div className="node">
            Campaign India
          </div>
        </div>

      </div>



      {/* SHOWCASE */}

      <section className="showcase-section">

        <h2>
          Insights That Matter
        </h2>

        <div className="showcase-grid">

          <div className="showcase-card">
            Discover Hidden Trends
          </div>

          <div className="showcase-card">
            Understand Customer Voice
          </div>

          <div className="showcase-card">
            Track Competitor Activity
          </div>

          <div className="showcase-card">
            Monitor Brand Reputation
          </div>

        </div>

      </section>

      {/* WHY */}

      <section className="why-section">

        <h2>
          Every Conversation Matters
        </h2>

        <p>

          Every post, article, review and discussion
          contains valuable signals.

          Our platform helps uncover those signals
          and convert them into meaningful insights.

        </p>

      </section>

      {/* CTA */}

      <section className="cta-section">

        <h2>
          Ready To Start Listening?
        </h2>

        <p>
          Monitor conversations across multiple
          platforms from one unified workspace.
        </p>

        <button className="primary-btn">
          Get Started
        </button>

      </section>

    </div>

  );

}