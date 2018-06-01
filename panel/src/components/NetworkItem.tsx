import { h } from 'hyperapp';
import { WifiNetwork } from '../api-client';

const React = { createElement: h };

interface NetworkItemProps {
  network: WifiNetwork;
  onConnectClick(): void;
}

export const NetworkItem = ({ network, onConnectClick }: NetworkItemProps) => {
  return (
    <li className='NetworkItem'>
      <span className='NetworkItem__ssid'>
        {network.ssid}
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
