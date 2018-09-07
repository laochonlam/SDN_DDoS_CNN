from mininet.topo import Topo

class CustomTopo( Topo ):
    
    def __init__( self ):
        Topo.__init__(self)

        s0 = self.addSwitch("s0")
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        
	# inside the network
        h0 = self.addHost("h0")
	h1 = self.addHost("h1")

	# attackers
        h2 = self.addHost("h2")
	h3 = self.addHost("h3")
	h4 = self.addHost("h4")
        
        self.addLink(s0, s1)
        self.addLink(s0, s2) 
	self.addLink(s0, h2)   
	self.addLink(s1, h0)
	self.addLink(s2, h1)
	self.addLink(s0, h3)
	self.addLink(s0, h4)

topos = { 'mytopo': (lambda: CustomTopo())} 
