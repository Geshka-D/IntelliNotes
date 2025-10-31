import { Toaster as SonnerToaster, ToasterProps } from "sonner";

const Toaster = (props: ToasterProps) => (
  <SonnerToaster richColors closeButton {...props} />
);

export { Toaster };
