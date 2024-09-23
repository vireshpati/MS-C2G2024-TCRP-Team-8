import { useState } from 'react';
import Calendar from 'react-calendar';
import { Value } from 'react-calendar/dist/cjs/shared/types';
import 'react-calendar/dist/Calendar.css';
import { tw } from 'twind';

const CalendarSection = () => {
  const [value, setValue] = useState<Value>(new Date());

  const onChange = (newDate: Value) => {
    setValue(newDate);
  };

  return (
    <div className={tw(`flex flex-col items-center justify-center`)}>
      <h2 className={tw(`text-xl font-bold mb-4`)}>Add Our Events to your Calendar!</h2>
      <iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=America%2FNew_York&bgcolor=%23ffffff&title=The%20Community%20Restoration%20Project%20Events&src=dGNycDQ3ODZAZ21haWwuY29t&src=ZW4udXNhI2hvbGlkYXlAZ3JvdXAudi5jYWxlbmRhci5nb29nbGUuY29t&color=%23039BE5&color=%230B8043" width="800" height="600" frameBorder="0" scrolling="no"></iframe>
    </div>
  );
};

export default CalendarSection;