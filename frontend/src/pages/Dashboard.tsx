import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/client';

interface ResourceCounts {
  users: number;
  files: number;
  queries: number;
}

interface RecentItem {
  id: string;
  name: string;
  type: string;
  createdAt: string;
}

const Dashboard: React.FC = () => {
  const [counts, setCounts] = useState<ResourceCounts | null>(null);
  const [recentItems, setRecentItems] = useState<RecentItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [countsResponse, recentItemsResponse] = await Promise.all([
          axios.get('/api/dashboard/counts'),
          axios.get('/api/dashboard/recent-items'),
        ]);
        setCounts(countsResponse.data);
        setRecentItems(recentItemsResponse.data);
      } catch (err) {
        setError('Failed to load dashboard data.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleQuickAction = (action: string) => {
    switch (action) {
      case 'upload':
        navigate('/upload');
        break;
      case 'chat':
        navigate('/chat');
        break;
      case 'users':
        navigate('/users');
        break;
      default:
        break;
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-red-500">{error}</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="text-lg font-semibold">Users</h2>
          <p className="text-2xl font-bold">{counts?.users || 0}</p>
        </div>
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="text-lg font-semibold">Files</h2>
          <p className="text-2xl font-bold">{counts?.files || 0}</p>
        </div>
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="text-lg font-semibold">Queries</h2>
          <p className="text-2xl font-bold">{counts?.queries || 0}</p>
        </div>
      </div>
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">Recent Items</h2>
        <div className="bg-white shadow rounded-lg p-4">
          {recentItems.length > 0 ? (
            <table className="w-full text-left">
              <thead>
                <tr>
                  <th className="border-b p-2">Name</th>
                  <th className="border-b p-2">Type</th>
                  <th className="border-b p-2">Created At</th>
                </tr>
              </thead>
              <tbody>
                {recentItems.map((item) => (
                  <tr key={item.id}>
                    <td className="border-b p-2">{item.name}</td>
                    <td className="border-b p-2">{item.type}</td>
                    <td className="border-b p-2">{new Date(item.createdAt).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-gray-500">No recent items found.</p>
          )}
        </div>
      </div>
      <div>
        <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={() => handleQuickAction('upload')}
            className="bg-blue-500 text-white py-2 px-4 rounded-lg shadow hover:bg-blue-600"
          >
            Upload Files
          </button>
          <button
            onClick={() => handleQuickAction('chat')}
            className="bg-green-500 text-white py-2 px-4 rounded-lg shadow hover:bg-green-600"
          >
            Start Chat
          </button>
          <button
            onClick={() => handleQuickAction('users')}
            className="bg-purple-500 text-white py-2 px-4 rounded-lg shadow hover:bg-purple-600"
          >
            Manage Users
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;