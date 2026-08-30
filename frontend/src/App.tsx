import { useState } from 'react';
import './App.css';

type Patient = {
  id: number;
  first_name: string;
  last_name: string;
  gender: string;
  street_address: string;
  city: string;
  state: string;
  zip_code: string;
  phone: string;
  diagnosis: string;
  gene: string;
};

type SearchTerm = {
  id: number;
  label: string;
  column: string;
  placeholder: string;
};

type QueryValues = Record<string, string>;

function App() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [searchTerms, ] = useState<SearchTerm[]>(
    [
      { id: 1, label: 'First Name', column: 'first_name', placeholder: 'Search first name...' },
      { id: 2, label: 'Last Name', column: 'last_name', placeholder: 'Search last name...' },
      { id: 3, label: 'State', column: 'state', placeholder: 'Search state (e.g. CA)...' },
      { id: 4, label: 'Cancer Diagnosis', column: 'diagnosis', placeholder: 'Search diagnosis...' },
      { id: 5, label: 'Genes', column: 'gene', placeholder: 'Search gene (e.g. BRCA1)...' }
    ]
  );


  const handleSearch = async (queryValues: QueryValues) => {
    const params = new URLSearchParams(queryValues).toString();
    
    const response = await fetch(`/api/patients?${params}`);
    const data = await response.json();
    setPatients(data);
  };

  return (
    <>
      <SearchBar searchTerms={searchTerms} handleSearch={handleSearch} />
      <PatientTable patients={patients} />
    </>
  );
}

interface SearchBarProps {
  searchTerms: SearchTerm[];
  handleSearch: (queryValues: QueryValues) => Promise<void>;
}

function SearchBar({ searchTerms, handleSearch }: SearchBarProps) {
  const [queryValues, setQueryValues] = useState<QueryValues>({});

  const handleInputChange = (column: string, value: string) => {
    setQueryValues((prev) => ({
      ...prev,
      [column]: value
    }));
  };

  return (
    <>
      <h2>Patient Database Search</h2>
      <div className="filter-container">
        {searchTerms.map((term) => (
          <SearchTerm 
            key={term.id} 
            term={term} 
            onInputChange={handleInputChange}
          />
        ))}

        <button id="search-button" onClick={() => handleSearch(queryValues)}>Search</button>
      </div>
    </>
  );
}

interface SearchTermProps {
  term: SearchTerm;
  onInputChange: (column: string, value: string) => void;
}
function SearchTerm({ term, onInputChange }: SearchTermProps) {
  return (
    <div className="filter-group">
      <label htmlFor={`filter-${term.id}`}>{term.label}</label>
      <input 
        type="text" 
        id={`filter-${term.id}`} 
        placeholder={term.placeholder} 
        onChange={(e) => onInputChange(term.column, e.target.value)}
      />
    </div>
  );
}

interface PatientTableProps {
  patients: Patient[];
}
function PatientTable({ patients }: PatientTableProps) {
  return (
    <table>
      <thead>
        <tr>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Gender</th>
          <th>Street Address</th>
          <th>City</th>
          <th>State</th>
          <th>Zip Code</th>
          <th>Phone</th>
          <th>Diagnosis</th>
          <th>Gene</th>
        </tr>
      </thead>
      <tbody>
        {patients.map((patient) => (
          <PatientRow key={patient.id} patient={patient} />
        ))}
      </tbody>
    </table>
  );
}

interface PatientRowProps {
  patient: Patient;
}
function PatientRow({ patient }: PatientRowProps) {
  return (
    <tr>
      <td>{patient.first_name}</td>
      <td>{patient.last_name}</td>
      <td>{patient.gender}</td>
      <td>{patient.street_address}</td>
      <td>{patient.city}</td>
      <td>{patient.state}</td>
      <td>{patient.zip_code}</td>
      <td>{patient.phone}</td>
      <td>{patient.diagnosis}</td>
      <td>{patient.gene}</td>
    </tr>
  );
}
export default App