export const fetchInternships = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/internships');
    if (!response.ok) {
      throw new Error('Failed to fetch internships');
    }
    return await response.json();
  };