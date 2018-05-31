import { h } from 'hyperapp';
import { ActionReturn, AppState, AppActions } from '../common';
import { WifiNetwork, ApiClient } from '../api-client';
import { NetworkList } from '../components/NetworkList';

const React = { createElement: h };

export interface ScanState {
  networks: WifiNetwork[] | 'unloaded' | 'loading';
}

export interface ScanActions {
  refresh(): ActionReturn<ScanState, ScanActions>;
  connect(network: WifiNetwork): ActionReturn<ScanState, ScanActions>;

  _setNetworks(networks: WifiNetwork[]): ActionReturn<ScanState, ScanActions>;
}

export const scanActions = (apiClient: ApiClient): ScanActions => ({
  refresh: () => (_, actions) => {
    apiClient.getNetworks().then(actions._setNetworks);

    return { networks: 'loading' };
  },

  connect: (network) => (_, __) => {
    const password = prompt('Please enter password');

    if (password === null) return;

    apiClient.connect(network.ssid, password);
  },

  _setNetworks: (networks: WifiNetwork[]) => () => ({ networks }),
});

export const Scan = () => ({ scan: { networks } }: AppState, { scan: { refresh, connect } }: AppActions) => {
  return (
    <div>

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
