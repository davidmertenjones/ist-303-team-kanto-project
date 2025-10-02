import { useState, useEffect } from "react";
// This tells TypeScript exactly what shape our data has
interface Facility {
  id: number;
  name: string;
  city: string;
  zip: string;
}

interface SearchParams {
  name: string;
  city: string;
  zip: string;
}

function App() {
  // services is an array of strings
  const [services, setServices] = useState<string[]>([]);
  
  //facilities is an array of Facility objects
  const [facilities, setFacilities] = useState<Facility[]>([]);
  
  //search matches the SearchParams interface
  const [search, setSearch] = useState<SearchParams>({ name: "", city: "", zip: "" });

  //Fetch services when component loads
  useEffect(() => {
    fetch("/api/services")
      .then(res => res.json())
      .then(data => setServices(data));
  }, []); // Empty array = run once when component mounts

  //Handle search button click
  const handleSearch = () => {
    // Convert search object to URL query string: ?name=...&city=...&zip=...
    const params = new URLSearchParams(search).toString();
    fetch(`/api/facilities?${params}`)
      .then(res => res.json())
      .then(data => setFacilities(data));
  };

  return (
    <div>
      <h1>Hospital Facilities Catalog</h1>
      
      <div>
        <input 
          placeholder="Name" 
          onChange={e => setSearch(s => ({ ...s, name: e.target.value }))} 
        />
        <input 
          placeholder="City" 
          onChange={e => setSearch(s => ({ ...s, city: e.target.value }))} 
        />
        <input 
          placeholder="ZIP" 
          onChange={e => setSearch(s => ({ ...s, zip: e.target.value }))} 
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      <h2>Available Services</h2>
      <ul>
        {services.map(s => <li key={s}>{s}</li>)}
      </ul>

      <h2>Facilities</h2>
      <ul>
        {facilities.map(f => (
          <li key={f.id}>
            {f.name} - {f.city} - {f.zip}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;