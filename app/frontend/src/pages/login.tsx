// import Page from '@/components/page';

// export default function Home() {
//   return <Page>this is the log-in page</Page>;
// }
import { useState } from 'react';
import { tw } from 'twind';
import Page from '@/components/page';

export default function Home() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <Page hideNavigation={true}>
      <div className={tw(`max-w-md mx-auto bg-white p-8 rounded-lg shadow-lg mt-10`)}>
        <h1 className={tw(`text-2xl font-bold text-center mb-6`)}>Login</h1>

        <form>
          <div className={tw(`mb-4`)}>
            <label className={tw(`block text-gray-700 text-sm font-bold mb-2`)} htmlFor="username">
              Username
            </label>
            <input
              className={tw(
                `shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-indigo-500`
              )}
              id="username"
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className={tw(`mb-6`)}>
            <label className={tw(`block text-gray-700 text-sm font-bold mb-2`)} htmlFor="password">
              Password
            </label>
            <input
              className={tw(
                `shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-indigo-500`
              )}
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div className={tw(`flex items-center justify-between`)}>
            <button
              type="submit"
              className={tw(
                `bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50`
              )}
            >
              Log In
            </button>
          </div>
        </form>
      </div>
    </Page>
  );
}