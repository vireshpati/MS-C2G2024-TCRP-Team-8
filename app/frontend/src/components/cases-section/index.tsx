import { tw } from 'twind';
import Particles from 'react-particles-js';
import Arrow from '@/constants/svg/arrow.svg';
import { useRouter } from 'next/router';

const ParticleBg = () => (
  <Particles
    params={{
      particles: {
        number: {
          value: 400,
          density: {
            enable: true,
            value_area: 3000,
          },
        },
        line_linked: {
          enable: false,
        },
        move: {
          direction: `right`,
          speed: 0.3,
        },
        size: {
          value: 1,
        },
        opacity: {
          anim: {
            enable: true,
            speed: 0.5,
            opacity_min: 0.1,
          },
        },
      },
      interactivity: {
        events: {
          onclick: {
            enable: false,
          },
        },
      },
      retina_detect: true,
    }}
  />
);

const articles = [
  {
    title: `Suggestions Portal.`,
    subtitle: 'Submit questions and concerns to CRP team.',
    image: `/images/case-1.webp`,
    alt: `Proident pariatur est.`,
    href: '/portal',
  },
  {
    title: `Find others.`,
    subtitle: 'Find similar members in the community.',
    image: `/images/case-2.webp`,
    alt: `Proident pariatur est.`,
    href: '/matches',
  },
  {
    title: `Chat.`,
    subtitle: 'Get all your questions answered.',
    image: `/images/case-3.webp`,
    alt: `Proident pariatur est.`,
    href: '/message',
  },
];

const CasesSection = () => {
  const router = useRouter();

  const handleClick = (href: string) => {
    router.push(href);
  };

  return (
  <section>
    <div className={tw(`w-full min-h-screen bg-maroon relative`)}>
      <div className={tw(`absolute left-0 top-0 h-screen w-full overflow-hidden`)}>
        <ParticleBg />
      </div>
      <div className={tw(`max-w-7xl mx-4 lg:mx-auto pt-20 lg:pt-40`)}>
        <h1 className={tw(`text-white text-4xl lg:text-7xl font-bold text-center`)}>Engage. Connect. Grow.</h1>
        <p className={tw(`text-white text-gray-400 text-center text-xl mt-12`)}>
          Use our features to seamlessly connect with your community, fostering engagement and collaboration through
          powerful tools.
        </p>
        <div className={tw(`mx-auto pt-24`)}>
          <div className={tw(`w-full flex flex-wrap justify-around`)}>
            {articles.map((article) => (
              <div
                key={article.title}
                className={tw(
                  `xl:w-1/3 sm:w-5/12 sm:max-w-xs relative mb-32 lg:mb-20
                      xl:max-w-sm lg:w-1/2 w-11/12 mx-auto sm:mx-0 cursor-pointer hover:scale-105`,
                )}
                onClick={() => handleClick(article.href)}
              >
                <div className={tw(`h-64 z-20`)}>
                  <img
                    src={article.image}
                    alt={article.alt}
                    className={tw(`h-full w-full object-cover overflow-hidden rounded`)}
                    width={400}
                    height={300}
                  />
                </div>
                <div className={tw(`p-4 shadow-lg w-full mx-auto -mt-8 bg-white rounded-b z-30 relative`)}>
                  {/* <p className={tw(`uppercase text-sm text-gray-700 text-center pb-1`)}>Case study</p> */}
                  <p className={tw(`text-gray-500 text-center pb-1 text-sm`)}>{article.title}</p>
                  <p className={tw(`text-gray-500 text-center pb-1 text-sm`)}>{article.subtitle}</p>
                </div>
              </div>
            ))}
            {/* <span
              className={tw(
                `-mt-8 pb-12 lg:mt-4 flex items-center text-xl
                text-indigo-400 cursor-pointer z-30 hover:text-indigo-600`,
              )}
            >
              See all case studies
              <Arrow className={tw(`h-6 w-6 fill-current ml-2`)} />
            </span> */}
          </div>
        </div>
      </div>
    </div>
  </section>
  );
};

export default CasesSection;
