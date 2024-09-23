import Head from 'next/head';
import Navigation from '@/components/navigation';
import { tw } from 'twind';
import Link from 'next/link';

interface IProps {
  children: React.ReactNode;
  hideNavigation?: boolean;
}

const Page = ({ children, hideNavigation }: IProps) => (
  <div>
    <Head>
      <link rel="icon" href="/logo.svg" />
    </Head>
    <div className={tw(`min-h-screen flex flex-col`)}>
      {/* <Navigation /> */}
      {!hideNavigation && <Navigation />}
      <div className={tw('bg-lightGrey')}>{children}</div>
    </div>
  </div>
);

export default Page;
