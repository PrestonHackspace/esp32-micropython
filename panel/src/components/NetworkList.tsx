import { h } from 'hyperapp';
import { WifiNetwork } from '../api-client';
import { NetworkItem } from './NetworkItem';

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
