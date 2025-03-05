import { useState } from 'react'
import Navbar from './components/Navbar'
import SideMenu from './components/SideMenu'
import ContentArea from './components/ContentArea'
import Chatbot from './components/Chatbot'
import './App.css'

function App() {
  const [selectedPage, setSelectedPage] = useState('Apps')
  const [searchTerm, setSearchTerm] = useState('')

  return (
    <div className="app">
      <Navbar onSearch={setSearchTerm} />
      <div className="main">
        <SideMenu onSelect={setSelectedPage} selected={selectedPage} />
        <ContentArea page={selectedPage} searchTerm={searchTerm} />
      </div>
      <Chatbot />
    </div>
  )
}

export default App
