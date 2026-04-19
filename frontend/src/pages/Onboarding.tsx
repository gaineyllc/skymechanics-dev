import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Cell, Grid } from 'baseui/layout-grid';
import { Button } from 'baseui/button';
import { Input } from 'baseui/input';
import { Select } from 'baseui/select';
import { Block } from 'baseui/block';
import { StatefulTooltip } from 'baseui/tooltip';

type AccountType = 'flight_school' | 'solo_owner' | 'fbo_shop';

const accountTypes = [
  { id: 'flight_school', label: 'Flight School', description: 'Multi-aircraft operation with instructors' },
  { id: 'solo_owner', label: 'Solo Owner', description: 'Single aircraft, personal use' },
  { id: 'fbo_shop', label: 'FBO / Maintenance Shop', description: 'Service provider for multiple clients' },
];

const headingStyles = {
  h1: {
    fontSize: '48px',
    fontWeight: '700',
    marginBottom: '8px',
    margin: '0 0 8px 0',
  },
  h3: {
    fontSize: '18px',
    color: '#666',
    margin: '0',
  },
  h4: {
    fontSize: '18px',
    fontWeight: '600',
    marginBottom: '12px',
    margin: '0 0 12px 0',
  },
  h5: {
    fontSize: '18px',
    fontWeight: '600',
    margin: '0',
  },
  p: {
    fontSize: '14px',
    margin: '0',
  },
};

export default function Onboarding() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [orgName, setOrgName] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [accountType, setAccountType] = useState<AccountType | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!accountType) {
      setError('Please select an account type');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:8080/api/v1/onboard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          account_type: accountType,
          org_name: orgName,
          first_name: firstName,
          last_name: lastName,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to create account');
      }

      const data = await response.json();
      // Store token for future requests
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('tenantId', data.tenant_id);

      // Redirect to onboarding success
      navigate('/onboarding-success');
    } catch (err: any) {
      setError(err.message || 'Failed to create account');
    } finally {
      setLoading(false);
    }
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
        >
          <Block marginBottom="32px">
            <div style={headingStyles.h1}>Welcome to SkyMechanics</div>
            <div style={headingStyles.h3}>Aircraft Maintenance Management Platform</div>
          </Block>

          <form onSubmit={handleSubmit}>
            <Block marginBottom="24px">
              <div style={headingStyles.h4}>Account Type</div>
              <Grid>
                {accountTypes.map((type) => (
                  <Cell span={12} key={type.id}>
                    <Block
                      onClick={() => setAccountType(type.id as AccountType)}
                      cursor="pointer"
                      padding="16px"
                      border="1px solid"
                      borderColor={accountType === type.id ? '#1a90ff' : '#ddd'}
                      borderRadius="8px"
                      backgroundColor={accountType === type.id ? '#e8f4ff' : 'white'}
                      transition="all 0.2s"
                    >
                      <div style={headingStyles.h5}>{type.label}</div>
                      <div style={headingStyles.p}>{type.description}</div>
                    </Block>
                  </Cell>
                ))}
              </Grid>
            </Block>

            {error && (
              <Block marginBottom="24px" backgroundColor="#ffe5e5" padding="12px" borderRadius="4px">
                <div style={headingStyles.p}>{error}</div>
              </Block>
            )}

            <Block marginBottom="24px">
              <Input
                label="Email Address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                required
              />
            </Block>

            <Block marginBottom="24px">
              <Input
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Minimum 8 characters"
                required
              />
            </Block>

            <Block marginBottom="24px">
              <Input
                label="Confirm Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Re-enter password"
                required
              />
            </Block>

            <Block marginBottom="24px">
              <Input
                label="Organization Name"
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
                placeholder="e.g., Sky Flight Academy"
                required
              />
            </Block>

            <Grid>
              <Cell span={6}>
                <Input
                  label="First Name"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  placeholder="John"
                  required
                />
              </Cell>
              <Cell span={6}>
                <Input
                  label="Last Name"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  placeholder="Doe"
                  required
                />
              </Cell>
            </Grid>

            <Block marginTop="32px">
              <Button
                kind="primary"
                isLoading={loading}
                fullWidth
                type="submit"
              >
                Get Started
              </Button>
            </Block>

            <Block marginTop="24px" textAlign="center">
              <div style={headingStyles.p}>
                Already have an account?{' '}
                <a href="/login" style={{ color: '#1a90ff' }}>
                  Log in
                </a>
              </div>
            </Block>
          </form>
        </Block>
      </Cell>
    </Grid>
  );
}
