import { NextRouter } from "next/router";

export const handleSubmit = (
  url: string,
  router: NextRouter
) => {
//   console.log(e.currentTarget["URL"].value);
  router.push(`/analyze?article=${url}`);
};
