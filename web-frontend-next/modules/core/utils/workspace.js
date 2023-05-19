import { isSecureURL } from "./string";

// NOTE: this has been deliberately left as `group`. A future task will rename it.
const cookieWorkspaceName = "baserow_group_id";

export const setWorkspaceCookie = (workspaceId, { $cookies, $env }) => {
  if (process.SERVER_BUILD) return;
  const secure = isSecureURL($env.PUBLIC_WEB_FRONTEND_URL);
  $cookies.set(cookieWorkspaceName, workspaceId, {
    path: "/",
    maxAge: 60 * 60 * 24 * 7,
    sameSite: "lax",
    secure,
  });
};

export const unsetWorkspaceCookie = ({ $cookies }) => {
  if (process.SERVER_BUILD) return;
  $cookies.remove(cookieWorkspaceName);
};

export const getWorkspaceCookie = ({ $cookies }) => {
  if (process.SERVER_BUILD) return;
  return $cookies.get(cookieWorkspaceName);
};
