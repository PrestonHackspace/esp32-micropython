import { h } from 'hyperapp';
import { ActionReturn, AppState, AppActions } from '../common';
import { ApiClient, DeviceStatus } from '../api-client';

const React = { createElement: h };

export interface StatusState {
  status: DeviceStatus | 'loading';
}

export interface StatusActions {
  loadStatus(): ActionReturn<StatusState, StatusActions>;

  _setStatus(status: DeviceStatus): ActionReturn<StatusState, StatusActions>;
}

export const statusActions = (apiClient: ApiClient): StatusActions => ({
  loadStatus: () => (_, actions) => {
    apiClient.getStatus().then(actions._setStatus);

    return { status: 'loading' };
  },

  _setStatus: (status) => () => ({ status }),
});

export const Status = () => ({ status: { status } }: AppState, { status: { loadStatus } }: AppActions) => {
  return (
    <div oncreate={loadStatus}>

      {
        status === 'loading' ?
          <div className='View__loading'>Loading...</div> :

          <div>
            <div>Access Point IP: {status.ap[0]}</div>

            {status.sta && <div>Network IP: {status.sta[0]}</div>}
          </div>
      }

      <div className='View__buttons'>
        <button onclick={loadStatus}>Refresh</button>
      </div>

    </div>
  );
};
