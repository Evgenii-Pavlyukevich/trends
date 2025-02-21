import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
`;

const Content = styled.div`
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
`;

const Title = styled.h1`
  font-family: 'Mulish', sans-serif;
  font-size: 24px;
  color: #232833;
  margin: 0;
`;

const PrivateContent = () => {
  return (
    <Container>
      <Content>
        <Title>Private Content</Title>
      </Content>
    </Container>
  );
};

export default PrivateContent; 