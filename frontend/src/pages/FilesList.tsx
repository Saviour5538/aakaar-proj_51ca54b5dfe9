import React, { useEffect, useState } from 'react';
import { getFiles, deleteFile } from '../api/client';
import { useNavigate } from 'react-router-dom';

interface File {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadedAt: string;
  status: string;
}

const FilesList: React.FC = () => {
  const [items, setItems] = useState<File[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState<string>('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFiles = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await getFiles();
        setItems(response);
      } catch (err) {
        setError('Failed to fetch files.');
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  const handleDelete = async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await deleteFile(id);
      setItems((prev) => prev.filter((file) => file.id !== id));
    } catch (err) {
      setError('Failed to delete file.');
    } finally {
      setLoading(false);
    }
  };

  const filteredItems = items.filter((file) =>
    file.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Files</h1>
        <button
          onClick={() => navigate('/files/new')}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Add New
        </button>
      </div>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search files..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-gray-300 rounded px-4 py-2 w-full"
        />
      </div>
      {loading && <div className="text-center">Loading...</div>}
      {error && <div className="text-red-500 text-center">{error}</div>}
      <table className="table-auto w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="border border-gray-300 px-4 py-2">Name</th>
            <th className="border border-gray-300 px-4 py-2">Size</th>
            <th className="border border-gray-300 px-4 py-2">Type</th>
            <th className="border border-gray-300 px-4 py-2">Uploaded At</th>
            <th className="border border-gray-300 px-4 py-2">Status</th>
            <th className="border border-gray-300 px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredItems.map((file) => (
            <tr key={file.id}>
              <td className="border border-gray-300 px-4 py-2">{file.name}</td>
              <td className="border border-gray-300 px-4 py-2">{file.size} KB</td>
              <td className="border border-gray-300 px-4 py-2">{file.type}</td>
              <td className="border border-gray-300 px-4 py-2">{file.uploadedAt}</td>
              <td className="border border-gray-300 px-4 py-2">{file.status}</td>
              <td className="border border-gray-300 px-4 py-2">
                <button
                  onClick={() => handleDelete(file.id)}
                  className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 mr-2"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FilesList;