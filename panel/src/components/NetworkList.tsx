import { h } from 'hyperapp';
import { WifiNetwork } from '../api-client';

const React = { createElement: h };

interface NetworkListProps {
  networks: WifiNetwork[];
  onConnectClick(network: WifiNetwork): void;
}

export const NetworkList = ({ networks, onConnectClick }: NetworkListProps) => {
  return (
    <div className='NetworkList'>
      <ul className='NetworkList__ul'>
        {
          networks.map(
            (network) => (
              <NetworkItem
                network={network}
                onConnectClick={() => onConnectClick(network)}
              />
            ),
          )
        }
      </ul>
    </div>
  );
};

interface NetworkItemProps {
  network: WifiNetwork;
  onConnectClick(): void;
}

const NetworkItem = ({ network, onConnectClick }: NetworkItemProps) => {
  return (
    <li className='NetworkItem'>
      <span className='NetworkItem__ssid'>
        {network.ssid} {network.saved ? '[Saved]' : null}
      </span>

      {
        network.rssi &&
        <span className='NetworkItem__rssi'>
          {network.rssi}db
        </span>
      }

      <button className='NetworkItem__connect' onclick={onConnectClick}>
        Connect
      </button>
    </li>
  );
};
