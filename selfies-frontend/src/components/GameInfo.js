import React, { useState } from 'react';
import { connect } from 'react-redux';
import { startRound } from '../modules/game';

function GameInfo({ game, dispatch, time }) {
  const [className, setCurrentClassName] = useState('bounce animated infinite');
  const beginRound = () => {
    dispatch(startRound());
    setCurrentClassName('');
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        marginRight: '1%',
        marginLeft: '1%',
        marginBottom: '1%',
        padding: '1%',
        maxHeight: '50vh',
        width: '10vw',
        justifyContent: 'center',
      }}
    >
      {!game.round_started && (
        <button className={className} type="button" onClick={beginRound}>
          START GAME!
        </button>
      )}
      {game.round_started && (
        <div style={{ textAlign: 'center' }}>
          seconds left
          <br />
          <h1 style={{ fontSize: '100px' }}>{time}</h1>
        </div>
      )}
    </div>
  );
}

export default connect()(GameInfo);