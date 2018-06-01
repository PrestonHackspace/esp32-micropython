import { h } from 'hyperapp';
import { ActionReturn, AppState, AppActions } from '../common';
import { WifiNetwork, ApiClient } from '../api-client';
import { NetworkList } from '../components/NetworkList';

const React = { createElement: h };

type Status = null | 'connecting' | 'connected' | 'failed';

export interface ScanState {
  networks: WifiNetwork[] | 'unloaded' | 'loading';

  status: Status;
}

export interface ScanActions {
  refresh(): ActionReturn<ScanState, ScanActions>;
  connect(network: WifiNetwork): ActionReturn<ScanState, ScanActions>;

  _setNetworks(networks: WifiNetwork[]): ActionReturn<ScanState, ScanActions>;
  _setStatus(status: Status): ActionReturn<ScanState, ScanActions>;
}

export const scanActions = (apiClient: ApiClient): ScanActions => ({
  refresh: () => (_, actions) => {
    apiClient.getNetworks().then(actions._setNetworks);

    return { networks: 'loading' };
  },

  connect: (network) => (_, actions) => {
    const password = prompt('Please enter password');

    if (password === null) return;

    apiClient.connect(network.ssid, password).then(({ status }) => {
      actions._setStatus(status);
    }).catch(() => {
      actions._setStatus('failed');
    });

    return { status: 'connecting' };
  },

  _setNetworks: (networks: WifiNetwork[]) => () => ({ networks }),

  _setStatus: (status) => () => ({ status }),
});

export const Scan = () => ({ scan: { networks, status } }: AppState, { scan: { refresh, connect } }: AppActions) => {
  return (
    <div oncreate={refresh}>

      {status && <div className={`View__status View__status--${status}`}>{status}</div>}

      {
        networks === 'unloaded' ?
          <div className='View__loading'>Press 'Refresh' to scan for networks</div> :

          networks === 'loading' ?
            <div className='View__loading'>Loading...</div> :

            <NetworkList networks={networks} onConnectClick={connect} />
      }

      <div className='View__buttons'>
        <button onclick={refresh}>Refresh</button>
      </div>

    </div>
  );
};
