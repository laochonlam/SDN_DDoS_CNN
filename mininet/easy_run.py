from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController
from functools import partial

def int2dpid( dpid ):
   try:
	  dpid = hex( dpid )[ 2: ]
	  dpid = '0' * ( 16 - len( dpid ) ) + dpid
	  return dpid
   except IndexError:
	  raise Exception( 'Unable to derive default datapath ID - '
					   'please either specify a dpid or use a '
			   'canonical switch name such as s23.' )


class CustomTopo( Topo ):
	
	def build( self, n=2 ):

		s0 = self.addSwitch("s0", dpid=int2dpid(1))
		# hidden parameter: protocols="OpenFlow13"
		# inside the network
		h0 = self.addHost("h0", ip='10.0.0.1', mac='00:00:00:00:01:00')
		h1 = self.addHost("h1", ip='10.0.0.2', mac='00:00:00:00:02:00')	
		
		self.addLink(s0, h0)
		self.addLink(s0, h1) 

def run():
	topo = CustomTopo( n=2 )
	net = Mininet(topo=topo, controller=RemoteController)
	# net.addNAT().configDefault()
	net.start()
	CLI(net)
	net.stop()

if __name__ == '__main__':
	run()