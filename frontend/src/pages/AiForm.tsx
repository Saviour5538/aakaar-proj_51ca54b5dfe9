import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createAi, updateAi, getAi } from '../api/client';

interface AiFormFields {
  name: string;
  description: string;
}

const AiForm: React.FC = () => {
  const { id } = useParams<{ id?: string }>();
  const [formData, setFormData] = useState<AiFormFields>({ name: '', description: '' });
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      const fetchAi = async () => {
        setLoading(true);
        setError(null);
        try {
          const response = await getAi(id);
          setFormData({ name: response.name, description: response.description });
        } catch (err) {
          setError('Failed to fetch AI details.');
        } finally {
          setLoading(false);
        }
      };

      fetchAi();
    }
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (id) {
        await updateAi(id, formData);
      } else {
        await createAi(formData);
      }
      navigate('/ai');
    } catch (err) {
      setError('Failed to save AI details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">{id ? 'Edit AI' : 'Create AI'}</h1>
      {loading && <div className="text-center">Loading...</div>}
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name" className="block font-medium mb-1">
            Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
        </div>
        <div>
          <label htmlFor="description" className="block font-medium mb-1">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
        </div>
        <div className="flex justify-end">
          <button
            type="button"
            onClick={() => navigate('/ai')}
            className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 mr-2"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Save
          </button>
        </div>
      </form>
    </div>
  );
};

export default AiForm;