import { tw } from 'twind';
import { useState } from 'react';
import Button from '@/components/button';
import Link from 'next/link';

interface IMenuButton {
  toggleMenu: React.MouseEventHandler<HTMLButtonElement>;
  showMenu: boolean;
}

type Link = {
  label: string;
  href: string;
};

const links = [
  {
    label: `Chatbot`,
    href: `/chatbot`,
  },
  {
    label: `Requests`,
    href: `/requests`,
  },
  {
    label: `Suggestions`,
    href: `/portal`,
  },
  {
    label: `Meet People`,
    href: `/meet`,
  },
  {
    label: `Your Matches!`,
    href: `/matches`,
  },
  {
    label: `Start Chatting`,
    href: `/message`,
  },
];

const secondaryLinks = [
  {
    label: `Log in`,
    href: `/login`,
  },
];

const MenuButton = ({ toggleMenu, showMenu }: IMenuButton) => (
  <button
    type="button"
    aria-controls="mobile-menu"
    aria-expanded={showMenu}
    onClick={toggleMenu}
    className={tw(`p-2 text-gray-400`)}
  >
    <span className={tw(`sr-only`)}>Open menu</span>
    {showMenu ? (
      <svg
        className={tw(`h-6 w-6`)}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        aria-hidden="true"
        width={24}
        height={24}
        href="/"
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
      </svg>
    ) : (
      <svg
        className={tw(`h-6 w-6`)}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        aria-hidden="true"
        width={24}
        height={24}
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    )}
  </button>
);

const MobileMenu = () => (
  <div className={tw(`md:hidden`)}>
    <div className={tw(`px-2 pt-2 pb-3 space-y-1 sm:px-3`)}>
      {links.map((link: Link) => (
        <a href={link.href} className={tw(`text-gray-500 block px-3 py-2 text-base font-medium`)} key={link.label}>
          {link.label}
        </a>
      ))}
    </div>
  </div>
);

const Navigation = () => {
  const [showMenu, setShowMenu] = useState(false);
  const toggleMenu = () => setShowMenu(!showMenu);
  const [showUserDropdown, setShowUserDropdown] = useState(false);

  const toggleUserDropdown = () => {
    setShowUserDropdown(!showUserDropdown);
  };

  const userData = {
    name: 'John Doe',
    birthday: 'January 1, 1990',
    role: 'Staff',
    email: 'johndoe@example.com',
    points: 150,
  };

  return (
    <nav className={tw(`bg-lunarGrey`)}>
      <div className={tw(`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`)}>
        <div className={tw(`flex items-center justify-between h-24`)}>
          <div className={tw(`flex items-center`)}>
            <div className={tw(`flex-shrink-0`)}>
              <Link href="/">
                <img className={tw(`h-12 w-12`)} src="logo.svg" alt="logo" width={48} height={48} />
              </Link>
            </div>
            <div className={tw(`hidden md:block`)}>
              <div className={tw(`ml-10 flex items-baseline space-x-4`)}>
                {links.map((link: Link) => (
                  <a
                    key={link.label}
                    href={link.href}
                    className={tw(
                      `text-white-200 hover:text-white-600 px-3 py-2 rounded-md font-medium border-b-2 border-transparent hover:border-maroon`,
                    )}
                  >
                    {link.label}
                  </a>
                ))}
              </div>
            </div>
          </div>
          <div className={tw(`flex items-center space-x-4`)}>
            <div className={tw(`relative`)}>
              <button onClick={toggleUserDropdown} className={tw(`flex items-center`)}>
                <img
                  className={tw(`h-10 w-10 rounded-full`)}
                  src="/blank_profile.png"
                  alt="User Profile"
                />
              </button>

              {showUserDropdown && (
                <div className={tw(`absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-2 z-50`)}>
                  <div className={tw(`px-4 py-2 text-sm text-gray-700`)}>Name: {userData.name}</div>
                  <div className={tw(`px-4 py-2 text-sm text-gray-700`)}>Role: {userData.role}</div>
                  <div className={tw(`px-4 py-2 text-sm text-gray-700`)}>Birthday: {userData.birthday}</div>
                  <div className={tw(`px-4 py-2 text-sm text-gray-700`)}>Email: {userData.email}</div>
                  <div className={tw(`px-4 py-2 text-sm text-gray-700`)}>Points: {userData.points}</div>
                </div>
              )}
            </div>

            <div className={tw(`-mr-2 flex md:hidden`)}>
              <MenuButton showMenu={showMenu} toggleMenu={toggleMenu} />
            </div>
          </div>
        </div>
      </div>
      {showMenu ? <MobileMenu /> : null}
    </nav>
  );
};

export default Navigation;
