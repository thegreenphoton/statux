import { useEffect, useState } from 'react';
import InternshipTable from '../components/InternshipTable';
import '../styles/HomePage.css';

export default function Home() {
    const [internships, setInternships] = useState([]);
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [internship, setInternship] = useState([]);
    const [showAddPopup, setShowAddPopup] = useState(false);
    const [showSearchPopup, setShowSearchPopup] = useState(false);
    const [formData, setFormData] = useState({
        company: '',
        position: '',
        status: '',
        date_applied: '',
    });

  useEffect(() => {

    async function fetchInternships() {
      try {
        //const response = await fetch(`https://statux-backend-591032654485.us-west1.run.app/api/internships`);
        const response = await fetch(`http://127.0.0.1:8080/api/internships`);
        const data = await response.json();

        
        setInternships(data);
      } catch (error) {
        console.error('Error fetching internships:', error);
      }
    }
    fetchInternships();
    
  }, []);

  const handleSearch = async () => {
    if (!query) {
        return;
    }

    try {
        //const response = await fetch(`https://statux-backend-591032654485.us-west1.run.app/api/search?company=${query}`);
        const response = await fetch(`http://127.0.0.1:8080/api/search?company=${query}`);
        if (response.ok) {
            const data = await response.json();
            setShowSearchPopup(true);
            setResults(data);
        }
        else {
            console.error('Failed to search for internships');
        }
  } catch (error) {
      console.error('Failed to search for internships:', error);
  }
};

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleDelete = async (id) => {
    try {
        /*const response = await fetch(`https://statux-backend-591032654485.us-west1.run.app/api/internships/${id}`, {
            method: 'DELETE',
        });*/
        const response = await fetch(`http://127.0.0.1:8080/api/internships/${id}`, {
            method: 'DELETE',
        });
        if (response.ok) {
            setInternship((prev) => prev.filter((internship) => internship.id !== id));
            console.log('Internship deleted');
            window.location.reload();
        }
        else {
            console.error('Failed to delete internship with id:', id);
        }
    }
    catch (error) {
        console.error('Failed to delete internship:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        //get date in correct time zone
        const date = new Date();
        const today = date.toLocaleDateString('en-CA');

        /*const response = await fetch(`https://statux-backend-591032654485.us-west1.run.app/api/internships`, {
            method: 'POST',
            headers:
                { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...formData,
                date_applied: today,
                status: "Applied"}),
         });*/
        
        const response = await fetch(`http://127.0.0.1:8080/api/internships`, {
            method: 'POST',
            headers:
                { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...formData,
                date_applied: today,
                status: "Applied"}),
         }); 
        if (response.ok) {
            const newInternship = await response.json();
            setInternship((prev) => [...prev, newInternship]);
            setShowAddPopup(false);
            window.location.reload();
        }
    }
    catch (error) {
        console.error('Failed to create internship:', error);
    }
};

  return (
    <div>







    <button className="add-button" onClick={() => setShowAddPopup(true)}>+</button>
      <h1 className="home-header">Statux</h1>
      <h3 className="home-subheader">Track your job applications</h3>

                  {/* Search Bar */}
                  <div style={{ marginBottom: '20px' }}>
                <input
                    type="text"
                    placeholder="Search by company name"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button onClick={handleSearch}>Search</button>
            </div>


            {/* Search Results Popup */}
            {showSearchPopup && (
                <div className="popup">
                    <div className="popup-content">
                        <button className="close-btn" onClick={() => setShowSearchPopup(false)}>
                            ×
                        </button>
                        <h2>Search Results</h2>
                        {results.length > 0 ? (
                            <ul>
                                {results.map((result) => (
                                    <li key={result.id}>
                                        <strong>{result.company}</strong> - {result.position} ({result.status})
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p>No results found</p>
                        )}
                    </div>
                </div>
            )}



      {showAddPopup && (
        <div className="popup">
          <form onSubmit={handleSubmit}>
            <h2>Add Internship</h2>
            <label>
              Company:
              <input
                type="text"
                name="company"
                value={formData.company}
                onChange={handleInputChange}
                required
              />
            </label>
            <label>
              Position:
              <input
                type="text"
                name="position"
                value={formData.position}
                onChange={handleInputChange}
                required
              />
            </label>
            <button type="submit">Submit</button>
            <button type="button" onClick={() => setShowAddPopup(false)}>
              Cancel
            </button>
          </form>
        </div>
      )}
      <InternshipTable internships={internships} onDelete={handleDelete} />
    </div>
  );
}