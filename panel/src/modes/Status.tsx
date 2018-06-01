import { h } from 'hyperapp';
import { ActionReturn, AppState, AppActions } from '../common';
import { ApiClient, DeviceStatus } from '../api-client';

const React = { createElement: h };

export interface StatusState {
  deviceStatus: DeviceStatus | 'loading';
}

export interface StatusActions {
  refresh(): ActionReturn<StatusState, StatusActions>;

  _setStatus(status: DeviceStatus): ActionReturn<StatusState, StatusActions>;
}

export const statusActions = (apiClient: ApiClient): StatusActions => ({
  refresh: () => (_, actions) => {
    apiClient.getStatus().then(actions._setStatus);

    return { deviceStatus: 'loading' };
  },

  _setStatus: (deviceStatus) => () => ({ deviceStatus }),
});

export const Status = () => ({ status: { deviceStatus } }: AppState, { status: { refresh } }: AppActions) => {
  return (
    <div>

      {
        deviceStatus === 'loading' ?
          <div className='View__loading'>Loading...</div> :

          <div className='Status__ips'>
            {deviceStatus.ap && <div>Access Point IP: {deviceStatus.ap[0]}</div>}

            {deviceStatus.sta && <div>Network IP: {deviceStatus.sta[0]}</div>}
          </div>
      }

      <div className='View__buttons'>
        <button onclick={refresh}>Refresh</button>
      </div>

    </div>
  );
};
