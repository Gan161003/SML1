import { useEffect, useState } from "react";
import axios from "axios";

import "../styles/Reports.css";

// const API = "http://127.0.0.1:8000";https://sml-backend-agdr.onrender.com/
const API = "https://sml-backend-agdr.onrender.com";

export default function Reports() {

  const [reportType, setReportType] =
    useState("executive");

  const [filterOptions,
    setFilterOptions] = useState({
      platforms: [],
      sentiments: [],
      brands: []
    });

  const [filters, setFilters] =
    useState({
      platform: "",
      sentiment: "",
      brand: "",
      keyword: ""
    });

  const [preview, setPreview] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  useEffect(() => {

    loadFilterOptions();

  }, []);

  async function loadFilterOptions() {

    try {

      const res = await axios.get(
        `${API}/dashboard/filter-options`
      );

      setFilterOptions(
        res.data
      );

    } catch (error) {

      console.log(error);

    }
  }



  const downloadCSV = () => {

  const query = new URLSearchParams(
    filters
  ).toString();

  window.open(
    `${API}/reports/download-csv?${query}`
  );

};


const downloadExcel = () => {

  const query = new URLSearchParams(
    filters
  ).toString();

  window.open(
    `${API}/reports/download-excel?${query}`
  );

};




  async function generatePreview() {

    try {

      setLoading(true);

      const res = await axios.get(
        `${API}/reports/preview`,
        {
          params: filters
        }
      );

      setPreview(
        res.data
      );

    } catch (error) {

      console.log(error);

    } finally {

      setLoading(false);

    }
  }

  function resetFilters() {

    setFilters({

      platform: "",

      sentiment: "",

      brand: "",

      keyword: ""

    });

    setPreview([]);

  }

  return (

    <div className="reports-page">

      <div className="reports-header">

        <h1>
          Reports Center
        </h1>

        <p>
          Generate Social Media Intelligence Reports
        </p>

      </div>

      {/* REPORT TYPE */}

      <div className="report-card">

        <label>
          Report Type
        </label>

        <select
          value={reportType}
          onChange={(e) =>
            setReportType(
              e.target.value
            )
          }
        >

          <option value="executive">
            Executive Summary
          </option>

          <option value="sentiment">
            Sentiment Analysis
          </option>

          <option value="brand">
            Brand Mention Report
          </option>

          <option value="platform">
            Platform Performance
          </option>

          <option value="keyword">
            Keyword Intelligence
          </option>

          <option value="hashtag">
            Hashtag Analytics
          </option>

          <option value="youtube">
            YouTube Analytics
          </option>

          <option value="instagram">
            Instagram Analytics
          </option>

          <option value="reputation">
            Reputation Risk
          </option>

        </select>

      </div>

      {/* FILTERS */}

      <div className="filters-grid">

        <div>

          <label>
            Platform
          </label>

          <select
            value={filters.platform}
            onChange={(e) =>
              setFilters({
                ...filters,
                platform:
                  e.target.value
              })
            }
          >

            <option value="">
              All Platforms
            </option>

            {filterOptions.platforms.map(
              (item, index) => (

                <option
                  key={index}
                  value={item}
                >
                  {item}
                </option>

              )
            )}

          </select>

        </div>

        <div>

          <label>
            Sentiment
          </label>

          <select
            value={filters.sentiment}
            onChange={(e) =>
              setFilters({
                ...filters,
                sentiment:
                  e.target.value
              })
            }
          >

            <option value="">
              All Sentiments
            </option>

            {filterOptions.sentiments.map(
              (item, index) => (

                <option
                  key={index}
                  value={item}
                >
                  {item}
                </option>

              )
            )}

          </select>

        </div>

        <div>

          <label>
            Brand
          </label>

          <select
            value={filters.brand}
            onChange={(e) =>
              setFilters({
                ...filters,
                brand:
                  e.target.value
              })
            }
          >

            <option value="">
              All Brands
            </option>

            {filterOptions.brands.map(
              (item, index) => (

                <option
                  key={index}
                  value={item}
                >
                  {item}
                </option>

              )
            )}

          </select>

        </div>

        <div>

          <label>
            Keyword Search
          </label>

          <input
            type="text"
            placeholder="Search..."
            value={filters.keyword}
            onChange={(e) =>
              setFilters({
                ...filters,
                keyword:
                  e.target.value
              })
            }
          />

        </div>

      </div>

      {/* ACTIONS */}

      <div className="report-actions">

        <button
          className="generate-btn"
          onClick={
            generatePreview
          }
        >
          Generate Preview
        </button>

        <button
          className="excel-btn"
          onClick={downloadExcel}
        >
          Download Excel
        </button>

       <button
          className="csv-btn"
          onClick={downloadCSV}
        >
          Download CSV
        </button>

        <button
          className="reset-btn"
          onClick={
            resetFilters
          }
        >
          Reset
        </button>

      </div>

      {/* PREVIEW */}

      {/* <div className="preview-card">

        <h3>
          Report Preview
        </h3>

        {loading ? (

          <p>
            Loading...
          </p>

        ) : (

          <div
            className="table-wrapper"
          >

            <table>

              <thead>

                <tr>

                  <th>
                    Platform
                  </th>

                  <th>
                    Keyword
                  </th>

                  <th>
                    Sentiment
                  </th>

                  <th>
                    Source File
                  </th>

                </tr>

              </thead>

              <tbody>

                {preview.map(
                  (
                    item,
                    index
                  ) => (

                    <tr
                      key={index}
                    >

                      <td>
                        {
                          item.platform
                        }
                      </td>

                      <td>
                        {
                          item.keyword
                        }
                      </td>

                      <td>
                        {
                          item.sentiment_label ||
                          item.sentiment
                        }
                      </td>

                      <td>
                        {
                          item.source_file
                        }
                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        )} */}

      {/* </div> */}

    </div>

  );

}
