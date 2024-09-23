import Page from '@/components/page';

import React, { useState } from 'react';



const Contact = ()  => {
  const [result, setResult] = React.useState("");

  const [formData, setFormData] = useState<SuggestionFormData>({
    email: '',
    subject: '',
    body: '',
    access_key: ''
  });
  
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState('');
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };
  

  const onSubmit = async (event) => {
    event.preventDefault();
    setResult("Sending....");
    const formData2 = new FormData(event.target);

    formData2.append("access_key", "117551ad-0229-4ffc-86a5-1f759a2208b8");

    const response = await fetch("https://api.web3forms.com/submit", {
      method: "POST",
      body: formData2
    });

    const data = await response.json();

    if (data.success) {
      setIsSubmitted(true);
      setFormData({ email: '', subject: '', body: '' });
    } else {
      setError('Failed to send suggestion. Please try again.');
    }
  };


  return (
<div style={{ width: '100%', display: 'flex', justifyContent: 'center', backgroundColor: '#f4f4f4', padding: '40px 0' }}>
  <div style={{ width: '300px', height: '430px', maxWidth: '100%', padding: '20px', backgroundColor: 'white', boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)', borderRadius: '8px', textAlign: 'center' }}>
    <h1>Suggestions Portal</h1>
    <form onSubmit={onSubmit}>
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="email">Your Email:</label><br />
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="subject">Subject:</label><br />
        <input
          type="text"
          id="subject"
          name="subject"
          value={formData.subject}
          onChange={handleInputChange}
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="body">Suggestion:</label><br />
        <textarea
          id="body"
          name="body"
          value={formData.body}
          onChange={handleInputChange}
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc', minHeight: '100px' }}
        />
      </div>

      <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
        Submit
      </button>
    </form>

    {isSubmitted && <p style={{ marginTop: '15px', color: 'green' }}>Thank you for your suggestion!</p>}
    {error && <p style={{ marginTop: '20px', color: 'red' }}>{error}</p>}
  </div>
</div>
  );
}


//export default SuggestionForm;
export default function Home() {
  return (
    <Page>
      <div className="min-h-screen flex iterms-center justify-center bg-gray-200">
        <Contact />
      </div>
    </Page>
  );
}
