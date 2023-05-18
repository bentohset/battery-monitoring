import React from 'react'

function Modal({modal}) {
  return (
    <>
    {modal ? (
        <div>Modal</div>
    ) : (
        <></>
    )} 
    </>
  )
}

export default Modal