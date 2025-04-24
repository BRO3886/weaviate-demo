import { ChangeEvent, useRef, useState } from "react";
import "./App.css";

function App() {
  const [searchType, setSearchType] = useState<"text" | "image">("text");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<any[] | null>(null);
  const [queryTime, setQueryTime] = useState<number | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  const handleTextSearch = async () => {
    if (!query.trim()) {
      setError("Please enter a search query");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/search-text`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query, top_k: 10 }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to search");
      }

      const data = await response.json();
      setResults(data.results);
      setQueryTime(data.query_time);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to search");
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  const handleImageSearch = async (file: File) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/search-image`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to search");
      }

      const data = await response.json();
      setResults(data.results);
      setQueryTime(data.query_time);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to search");
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleSearch = () => {
    if (searchType === "text") {
      handleTextSearch();
    } else if (selectedFile) {
      handleImageSearch(selectedFile);
    } else if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Image Search</h1>

      <div className="mb-6">
        <div className="flex items-center mb-4">
          <div className="mr-4">
            <label className="flex items-center">
              <input
                type="radio"
                value="text"
                checked={searchType === "text"}
                onChange={() => {
                  setSearchType("text");
                  setSelectedFile(null);
                }}
                className="mr-2"
              />
              <span>Text Search</span>
            </label>
          </div>
          <div>
            <label className="flex items-center">
              <input
                type="radio"
                value="image"
                checked={searchType === "image"}
                onChange={() => setSearchType("image")}
                className="mr-2"
              />
              <span>Image Search</span>
            </label>
          </div>
        </div>

        <div className="flex">
          {searchType === "text" ? (
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter search query..."
              className="flex-grow border rounded px-3 py-2 mr-2"
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
          ) : (
            <div
              onClick={() => fileInputRef.current?.click()}
              className="flex-grow border rounded px-3 py-2 mr-2 bg-gray-100 flex items-center image-upload-placeholder"
            >
              {selectedFile ? (
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-gray-200 rounded flex items-center justify-center mr-2">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      className="w-6 h-6"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                  </div>
                  <span className="truncate">{selectedFile.name}</span>
                  <button
                    className="ml-2 text-red-500 text-sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedFile(null);
                    }}
                  >
                    ✕
                  </button>
                </div>
              ) : (
                <span className="text-gray-500">
                  Click to upload an image...
                </span>
              )}
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleImageUpload}
                accept="image/jpeg,image/png,image/jpg"
                className="hidden"
              />
            </div>
          )}
          <button
            onClick={handleSearch}
            className="bg-blue-500 text-white px-4 py-2 rounded"
            disabled={loading || (searchType === "image" && !selectedFile)}
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>

        {error && <div className="mt-2 text-red-600">{error}</div>}
      </div>

      {results && (
        <div className="grid grid-cols-1 gap-4">
          <div className="border rounded p-4 results-container">
            <h2 className="text-xl font-semibold mb-2">Results</h2>
            {queryTime && (
              <p className="text-sm text-gray-500 mb-2">
                Query time: {queryTime.toFixed(2)}ms
              </p>
            )}
            <div className="space-y-4">
              {results.length === 0 ? (
                <div className="text-gray-500">No results found</div>
              ) : (
                results.map((result, index) => (
                  <div key={index} className="border-b pb-2">
                    {result.image_url && (
                      <img
                        src={`${API_BASE_URL}/${result.image_url}`}
                        alt={result.caption || `Result ${index}`}
                        className="h-32 object-contain mb-2"
                      />
                    )}
                    {result.caption && <p>{result.caption}</p>}
                    <p className="text-sm text-gray-600">
                      Score: {result.score?.toFixed(4) || "N/A"}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
