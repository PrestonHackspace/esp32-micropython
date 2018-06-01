import { h } from 'hyperapp';
import { ActionReturn, StatefulView } from '../common';
import { WifiNetwork, ApiClient } from '../api-client';
import { NetworkList } from '../components/NetworkList';

const React = { createElement: h };

type Status = null | 'connecting' | 'connected' | 'failed';

export interface SavedState {
  networks: WifiNetwork[] | 'unloaded' | 'loading';

  status: Status;
}

export interface SavedActions {
  refresh(): ActionReturn<SavedState, SavedActions>;
  connect(network: WifiNetwork): ActionReturn<SavedState, SavedActions>;

  _setNetworks(networks: WifiNetwork[]): ActionReturn<SavedState, SavedActions>;
  _setStatus(status: Status): ActionReturn<SavedState, SavedActions>;
}

export const savedActions = (apiClient: ApiClient): SavedActions => ({
  refresh: () => (_, actions) => {
    apiClient.getSavedNetworks().then(actions._setNetworks);

    return { networks: 'loading' };
  },

  connect: (network) => (_, actions) => {
    if (!network.rssi) {
      alert('This network is not within range');

      return;
    }

    apiClient.connectSaved(network.ssid).then(() => {
      actions._setStatus('connected');
    }).catch(() => {
      actions._setStatus('failed');
    });

    return { status: 'connecting' };
  },

  _setNetworks: (networks) => () => ({ networks }),

  _setStatus: (status) => () => ({ status }),
});

export const Saved: StatefulView = () => ({ saved: { networks, status } }, { saved: { refresh, connect } }) => {
  return (
    <div>

      <div className={`View__status View__status--${status}`}>{status}</div>

      {
        networks === 'unloaded' ?
          <div className='View__loading'>Press 'Refresh' to view saved networks</div> :

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
