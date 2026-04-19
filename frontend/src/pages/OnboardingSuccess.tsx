import { useNavigate } from 'react-router-dom';
import { Cell, Grid } from 'baseui/layout-grid';
import { Button } from 'baseui/button';
import { Block } from 'baseui/block';
import { Check } from 'baseui/icon';

const headingStyles = {
  h1: {
    fontSize: '36px',
    fontWeight: '700',
    margin: '0 0 16px 0',
  },
  h3: {
    fontSize: '18px',
    color: '#666',
    margin: '0 0 32px 0',
  },
  h4: {
    fontSize: '16px',
    fontWeight: '600',
    marginBottom: '16px',
    margin: '0 0 16px 0',
  },
  p: {
    fontSize: '14px',
    margin: '0',
  },
};

export default function OnboardingSuccess() {
  const navigate = useNavigate();

  const handleAddAircraft = () => {
    navigate('/quick-start');
  };

  const handleSkipToDashboard = () => {
    navigate('/dashboard');
  };

  return (
    <Grid style={{ minHeight: '100vh', background: '#f5f5f5' }}>
      <Cell span={12}>
        <Block
          marginLeft="auto"
          marginRight="auto"
          maxWidth="600px"
          padding="48px"
          marginTop="64px"
          backgroundColor="white"
          borderRadius="8px"
          boxShadow="0 4px 12px rgba(0,0,0,0.1)"
          textAlign="center"
        >
          <Block marginBottom="32px">
            <Check size="96px" color="#27b556" />
          </Block>

          <Block marginBottom="16px">
            <div style={headingStyles.h1}>Setup Complete!</div>
          </Block>

          <Block marginBottom="32px">
            <div style={headingStyles.h3}>
              Your SkyMechanics account is ready. Let's get you started!
            </div>
          </Block>

          <Block marginBottom="32px">
            <div style={headingStyles.h4}>What would you like to do next?</div>
            <Grid>
              <Cell span={12}>
                <Button
                  kind="primary"
                  onClick={handleAddAircraft}
                  fullWidth
                  marginBottom="16px"
                >
                  <Block display="flex" alignItems="center" justifyContent="center" gap="8px">
                    <Block fontSize="20px">✈️</Block>
                    Add Your First Aircraft
                  </Block>
                </Button>
              </Cell>
              <Cell span={12}>
                <Button
                  kind="secondary"
                  onClick={handleSkipToDashboard}
                  fullWidth
                >
                  <Block display="flex" alignItems="center" justifyContent="center" gap="8px">
                    <Block fontSize="20px">📊</Block>
                    Skip to Dashboard
                  </Block>
                </Button>
              </Cell>
            </Grid>
          </Block>

          <Block marginTop="24px" padding="16px" backgroundColor="#f5f5f5" borderRadius="8px">
            <div style={headingStyles.p}>
              <strong>Tip:</strong> Adding aircraft and mechanics now will let you create your first
              job immediately.
            </div>
          </Block>
        </Block>
      </Cell>
    </Grid>
  );
}
